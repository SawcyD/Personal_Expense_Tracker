document.getElementById('add-bank-btn').addEventListener('click', function() {
    // Perform any necessary AJAX request or redirect to the 'add_bank' URL
    var addBankUrl = this.dataset.addBankUrl;
    window.location.href = addBankUrl;
});

var savingsProgressData = [{
    type: 'indicator',
    mode: 'gauge+number',
    value: {{ savings_progress }},
    title: { text: 'Savings Progress' },
    gauge: {
        axis: { range: [null, {{ savings_goal }}] },
        bar: { color: 'rgba(100, 150, 200, 0.6)' },
        bgcolor: 'white',
        borderwidth: 2,
        bordercolor: 'gray',
        steps: [
            { range: [0, {{ savings_goal * 0.5 }}], color: 'rgba(150, 200, 250, 0.8)' },
            { range: [{{ savings_goal * 0.5 }}, {{ savings_goal }}], color: 'rgba(100, 150, 200, 0.8)' }
        ]
    }
}];

var savingsProgressLayout = { width: 400, height: 300 };
Plotly.newPlot('savings-progress-chart', savingsProgressData, savingsProgressLayout);

// Script to render the expense distribution chart
var expenseDistributionData = [
    // Expense distribution data
];

var expenseDistributionLayout = { width: 500, height: 400 };
Plotly.newPlot('expense-distribution-chart', expenseDistributionData, expenseDistributionLayout);

// Script to handle tab switching
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab-item');
    const sections = document.querySelectorAll('.dashboard-section');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetSection = tab.dataset.section;
            activateTab(targetSection);
        });
    });

    // Activate the first tab by default
    activateTab('overview');

    function activateTab(section) {
        tabs.forEach(tab => {
            tab.classList.remove('active');
        });

        sections.forEach(section => {
            section.classList.remove('active');
        });

        const targetTab = document.querySelector(`[data-section="${section}"]`);
        const targetSection = document.getElementById(`${section}-section`);

        targetTab.classList.add('active');
        targetSection.classList.add('active');
    }
});

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    // Hide all tab contents
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Deactivate all tab links
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Display the selected tab content
    document.getElementById(tabName).style.display = "block";

    // Activate the selected tab link
    evt.currentTarget.className += " active";
}
