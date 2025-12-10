document.addEventListener("DOMContentLoaded", function() {

    // menu toggle
    window.toggleMenu = function() {
        document.getElementById("menu")?.classList.toggle("show");
    }

    // temporary line chart
    const ctx = document.getElementById('progressChart')?.getContext('2d');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Problems Solved',
                    data: [12, 19, 25, 32, 45, 52],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.1)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // card hover effect
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', () => card.style.transform = 'translateY(-2px)');
        card.addEventListener('mouseleave', () => card.style.transform = 'translateY(0)');
    });

    $('#example-forms').on('input', 'textarea', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

});
