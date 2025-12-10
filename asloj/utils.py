import subprocess
import tempfile
import os
import shutil
import signal

SUPPORTED_EXTENSIONS = {
    "py": ".py",
    "c": ".c",
    "cpp": ".cpp",
    "java": ".java",
    "js": ".js",
}

def check_submission(problem, code_path, language, time_limit):
    language = language.lower().strip()
    results = []

    if language not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported language: {language}")

    inputs = list(problem.test_inputs.all().order_by("id"))
    outputs = list(problem.test_outputs.all().order_by("id"))
    testcases = list(zip(inputs, outputs))


    work_dir = tempfile.mkdtemp()
    exe_file = None

    try:
        # -------------------------
        # Compile / Prepare Code
        # -------------------------
        if language == "py":
            cmd_template = ["python", code_path]

        elif language in ["c", "cpp"]:
            ext = ".c" if language == "c" else ".cpp"
            base_name = os.path.basename(code_path)

            if not base_name.lower().endswith(ext):
                temp_path = os.path.join(work_dir, f"Main{ext}")
                shutil.copy(code_path, temp_path)
                code_path = temp_path

            exe_file = os.path.join(work_dir, "a.exe")
            compiler = "gcc" if language == "c" else "g++"

            compile_proc = subprocess.run(
                [compiler, code_path, "-o", exe_file],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return [{
                    "input": "",
                    "expected": "",
                    "actual": "",
                    "stderr": compile_proc.stderr.strip(),
                    "passed": False,
                    "verdict": "CE"
                }]

            cmd_template = [exe_file]

        elif language == "java":
            class_name = "Main"
            temp_java_path = os.path.join(work_dir, f"{class_name}.java")
            shutil.copy(code_path, temp_java_path)

            compile_proc = subprocess.run(
                ["javac", temp_java_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return [{
                    "input": "",
                    "expected": "",
                    "actual": "",
                    "stderr": compile_proc.stderr.strip(),
                    "passed": False,
                    "verdict": "CE"
                }]

            cmd_template = ["java", "-cp", work_dir, class_name]

        elif language == "js":
            cmd_template = ["node", code_path]

        # -------------------------
        # Normalize Output
        # -------------------------
        def normalize_output(s):
            return "\n".join(line.strip() for line in s.strip().splitlines() if line.strip())

        # -------------------------
        # Run each testcase
        # -------------------------
        for test_input, test_output in testcases:
            with open(test_input.file.path, "r", encoding="utf-8", errors="replace") as f:
                input_data = f.read()
            with open(test_output.file.path, "r", encoding="utf-8", errors="replace") as f:
                expected_output = f.read()

            try:
                # Use Popen for timeout-safe execution
                proc = subprocess.Popen(
                    cmd_template,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                try:
                    stdout, stderr = proc.communicate(input=input_data, timeout=time_limit)
                except subprocess.TimeoutExpired:
                    # Kill entire process tree
                    if os.name == "nt":
                        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)

                    stdout, stderr = "", "Time Limit Exceeded"
                    verdict = "TLE"
                else:
                    # Normal completion
                    if proc.returncode != 0:
                        verdict = "RE"
                    elif normalize_output(stdout) == normalize_output(expected_output):
                        verdict = "AC"
                    else:
                        verdict = "WA"

                results.append({
                    "input": input_data.strip(),
                    "expected": expected_output.strip(),
                    "actual": stdout.strip(),
                    "stderr": stderr.strip(),
                    "passed": verdict == "AC",
                    "verdict": verdict
                })

            except Exception as e:
                results.append({
                    "input": input_data.strip(),
                    "expected": expected_output.strip(),
                    "actual": "",
                    "stderr": str(e),
                    "passed": False,
                    "verdict": "RE"
                })

    finally:
        if exe_file and os.path.exists(exe_file):
            os.remove(exe_file)
        shutil.rmtree(work_dir, ignore_errors=True)

    return results



def judge_contest_submission(submission):
    """
    Judge a ContestSubmission by running it against the problem's test cases.
    Returns (verdict, points, results) where results is a list of dicts per testcase.
    """
    problem = submission.problem
    language = submission.language.lower().strip()
    code_path = submission.code_file.path
    time_limit = problem.time_limit
    results = []

    # Supported languages
    if language not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported language: {language}")

    test_inputs = list(problem.test_inputs.all().order_by("id"))
    test_outputs = list(problem.test_outputs.all().order_by("id"))
    testcases = list(zip(test_inputs, test_outputs))

    work_dir = tempfile.mkdtemp()
    exe_file = None

    try:
        # -------------------------
        # Compile / Prepare Code
        # -------------------------
        if language == "py":
            cmd_template = ["python", code_path]

        elif language in ["c", "cpp"]:
            ext = ".c" if language == "c" else ".cpp"
            base_name = os.path.basename(code_path)

            if not base_name.lower().endswith(ext):
                temp_path = os.path.join(work_dir, f"Main{ext}")
                shutil.copy(code_path, temp_path)
                code_path = temp_path

            exe_file = os.path.join(work_dir, "a.exe")
            compiler = "gcc" if language == "c" else "g++"

            compile_proc = subprocess.run(
                [compiler, code_path, "-o", exe_file],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return "CE", 0, [{
                    "input": "",
                    "expected": "",
                    "actual": "",
                    "stderr": compile_proc.stderr.strip(),
                    "passed": False,
                    "verdict": "CE"
                }]

            cmd_template = [exe_file]

        elif language == "java":
            class_name = "Main"
            temp_java_path = os.path.join(work_dir, f"{class_name}.java")
            shutil.copy(code_path, temp_java_path)

            compile_proc = subprocess.run(
                ["javac", temp_java_path],
                capture_output=True,
                text=True
            )

            if compile_proc.returncode != 0:
                return "CE", 0, [{
                    "input": "",
                    "expected": "",
                    "actual": "",
                    "stderr": compile_proc.stderr.strip(),
                    "passed": False,
                    "verdict": "CE"
                }]

            cmd_template = ["java", "-cp", work_dir, class_name]

        elif language == "js":
            cmd_template = ["node", code_path]

        # -------------------------
        # Normalize output function
        # -------------------------
        def normalize_output(s):
            return "\n".join(line.strip() for line in s.strip().splitlines() if line.strip())

        # -------------------------
        # Run each testcase
        # -------------------------
        passed_count = 0

        for test_input, test_output in testcases:
            with open(test_input.file.path, "r", encoding="utf-8", errors="replace") as f:
                input_data = f.read()
            with open(test_output.file.path, "r", encoding="utf-8", errors="replace") as f:
                expected_output = f.read()

            try:
                proc = subprocess.Popen(
                    cmd_template,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                try:
                    stdout, stderr = proc.communicate(input=input_data, timeout=time_limit)
                except subprocess.TimeoutExpired:
                    if os.name == "nt":
                        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    stdout, stderr = "", "Time Limit Exceeded"
                    verdict = "TLE"
                else:
                    if proc.returncode != 0:
                        verdict = "RE"
                    elif normalize_output(stdout) == normalize_output(expected_output):
                        verdict = "AC"
                        passed_count += 1
                    else:
                        verdict = "WA"

                results.append({
                    "input": input_data.strip(),
                    "expected": expected_output.strip(),
                    "actual": stdout.strip(),
                    "stderr": stderr.strip(),
                    "passed": verdict == "AC",
                    "verdict": verdict
                })

            except Exception as e:
                results.append({
                    "input": input_data.strip(),
                    "expected": expected_output.strip(),
                    "actual": "",
                    "stderr": str(e),
                    "passed": False,
                    "verdict": "RE"
                })

        # -------------------------
        # Determine final verdict and points
        # -------------------------
        if not results:
            final_verdict = "P"
            points = 0
        elif all(r["verdict"] == "AC" for r in results):
            final_verdict = "AC"
            points = 100
        else:
            final_verdict = "WA"
            points = int(100 * passed_count / len(results))

    finally:
        if exe_file and os.path.exists(exe_file):
            os.remove(exe_file)
        shutil.rmtree(work_dir, ignore_errors=True)

    return final_verdict, points, results


from django.db.models import Sum
from .models import ContestRegistration, ContestSubmission

def update_points(user, contest):
    """
    Update both contest registration points and user's overall points.
    """
    # Update contest registration points
    registration, _ = ContestRegistration.objects.get_or_create(
        user=user,
        contest=contest,
        defaults={
            'points': 0,
            'name': user.full_name,
            'email': user.email,
            'student_id': user.university_id
        }
    )
    registration.points = contest.user_points(user)
    registration.save()

    # Update user's overall points
    total_points = ContestSubmission.objects.filter(
        user=user,
        status='AC'
    ).aggregate(total=Sum('points'))['total'] or 0
    user.points = total_points
    user.save()


# utils.py
from datetime import timedelta
from django.utils import timezone
from collections import defaultdict
from .models import Submission


def generate_heatmap_data(user):
    """Generate daily AC submission counts for the past year."""
    today = timezone.now().date()
    start_date = today - timedelta(days=365)

    # Fetch accepted submissions in the past year
    submissions = (
        Submission.objects.filter(user=user, status='AC', created_at__date__gte=start_date)
        .values_list('created_at', flat=True)
    )

    # Count number of submissions per day
    daily_counts = defaultdict(int)
    for sub_date in submissions:
        day = sub_date.date()
        daily_counts[day] += 1

    # Prepare ordered list (for each day)
    heatmap_data = []
    for i in range(366):
        day = start_date + timedelta(days=i)
        count = daily_counts.get(day, 0)
        heatmap_data.append({
            'date': day.isoformat(),
            'count': count,
        })

    return heatmap_data
