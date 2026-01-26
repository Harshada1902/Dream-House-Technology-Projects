document.addEventListener("DOMContentLoaded", function () {

    // ---------- BAR CHART ----------
    const barCtx = document.getElementById("barChart");
    if (barCtx) {
        new Chart(barCtx, {
            type: "bar",
            data: {
                labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                datasets: [{
                    label: "Donations",
                    data: [45,60,55,70,90,110,95,85,100,120,130,150],
                    backgroundColor: "#dc3545"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // ---------- LINE CHART ----------
    const lineCtx = document.getElementById("lineChart");
    if (lineCtx) {
        new Chart(lineCtx, {
            type: "line",
            data: {
                labels: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                datasets: [{
                    label: "Donation Trend",
                    data: [30,40,50,60,75,85,95,110,120,130,140,160],
                    borderColor: "#0d6efd",
                    backgroundColor: "rgba(13,110,253,0.2)",
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    // ---------- PIE CHART ----------
    const pieCtx = document.getElementById("pieChart");
    if (pieCtx) {
        new Chart(pieCtx, {
            type: "pie",
            data: {
                labels: ["A+","A-","B+","B-","O+","O-","AB+","AB-"],
                datasets: [{
                    data: [150,50,120,30,200,70,40,20],
                    backgroundColor: [
                        "#dc3545", "#ff6b6b", "#0d6efd", "#6ea8fe",
                        "#198754", "#75b798", "#6f42c1", "#c29ffa"
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

});
