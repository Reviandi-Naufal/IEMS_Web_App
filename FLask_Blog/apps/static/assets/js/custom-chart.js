const headers = {
    headers: {'Content-Type': 'application/json'}
}
fetch("/api/real_data", {
        method: "GET",
        headers: headers
        }).then(response => response.json())
        .then(data => {
                        const x = data['data'].map(function(d){ return d['Date']})
                        const y = data['data'].map(function(d){ return d['Kwh']})
                        const chart_data = {
                            labels: x,
                            datasets: [{
                            label: 'Kwh Real Data',
                            backgroundColor: 'rgb(255, 99, 132)',
                            borderColor: 'rgb(255, 99, 132)',
                            data: y,
                            }]
                        };
                        const config = {
                            type: 'line',
                            data: chart_data,
                            options: {}
                        };
                        const linechart = new Chart(
                            document.getElementById('linechart'),
                            config
                        );
                        console.log(config)
                    });