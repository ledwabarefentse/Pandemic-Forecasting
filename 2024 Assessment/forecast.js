// Automatically download the table data as a CSV file
function downloadCSV() {
    const table = document.querySelector('#forecast-table tbody');
    let csvContent = 'Date,New Cases,Total Cases\n';

    // Loop through each row of the table
    table.querySelectorAll('tr').forEach(row => {
        const cells = row.querySelectorAll('td');
        let rowData = Array.from(cells).map(cell => cell.innerText).join(',');
        csvContent += rowData + '\n';
    });

    // Create a blob from the CSV content
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    // Create a link to trigger the download
    const a = document.createElement('a');
    a.href = url;
    a.download = 'forecast_table.csv';
    document.body.appendChild(a);
    a.click();

    // Clean up by removing the link
    document.body.removeChild(a);
}

// Automatically download the first graph (forecast plot) as PNG
function downloadPNG() {
    Plotly.downloadImage('forecast-plot', {
        format: 'png',
        width: 800,
        height: 600,
        filename: 'forecast_plot'
    });
}

// Automatically download a text file with advice on improving the system
function downloadTxt() {
    const adviceContent = `
    Advice for Improving Forecast Accuracy:

    1. Include demographic data:
       By incorporating population data by age group, region, and health conditions, we can understand which areas are more vulnerable and fine-tune the forecasts.
       
    2. Incorporate mobility data:
       Data on how people move between regions or countries could be included to understand how the virus spreads geographically.

    3. Vaccination rates:
       Including vaccination data will help account for the reduced spread and impact of the virus due to immunity in the population.

    4. Climate data:
       Certain viruses are more active in particular climates. Including weather data (such as temperature and humidity) could enhance the model's accuracy.

    5. Testing rates:
       Understanding how much testing is being conducted gives context to case data and may explain fluctuations in the data.

    6. Incorporate hospitalizations and death rates:
       These indicators provide more insights into the severity and outcomes of the virus, which can help improve the accuracy of the model's predictions.
    `;

    // Create a blob from the text content
    const blob = new Blob([adviceContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);

    // Create a link to trigger the download
    const a = document.createElement('a');
    a.href = url;
    a.download = 'forecast_improvement_advice.txt';
    document.body.appendChild(a);
    a.click();

    // Clean up by removing the link
    document.body.removeChild(a);
}


// Fetch forecasted data (7-day forecast) and original data
fetch('http://127.0.0.1:5000/forecast')
    .then(response => response.json())
    .then(forecastData => {
        fetch('http://127.0.0.1:5000/original')
            .then(response => response.json())
            .then(originalData => {
                const tableBody = document.querySelector('#forecast-table tbody');
                let plotDataX = [];  // For original data (dates)
                let newCasesY = [];  // For original daily new cases
                let forecastNewCasesX = []; // For forecasted dates (new cases)
                let forecastNewCasesY = []; // For forecasted daily new cases
                let cumulativeCasesY = []; // For original cumulative cases
                let forecastCumulativeX = []; // For forecasted dates (cumulative)
                let forecastCumulativeY = []; // For forecasted cumulative cases

                // Populate the forecast table (7-day forecast)
                Object.keys(forecastData).forEach(date => {
                    let forecastedRow = forecastData[date];

                    // Add forecasted data to the forecast table
                    let row = `<tr>
                        <td>${date}</td>
                        <td>${Math.round(forecastedRow['New Cases'])}</td>
                        <td>${Math.round(forecastedRow['Cumulative Cases'])}</td>
                    </tr>`;
                    tableBody.innerHTML += row;

                    // Data for 7-day forecast plot
                    forecastNewCasesX.push(date);
                    forecastNewCasesY.push(Math.round(forecastedRow['New Cases']));
                    forecastCumulativeX.push(date);
                    forecastCumulativeY.push(Math.round(forecastedRow['Cumulative Cases']));
                });

                // Populate original data for new cases and cumulative cases
                for (let i = 1; i < originalData.data.length; i++) {
                    const previousDayCases = originalData.data[i - 1].Cases;
                    const currentDayCases = originalData.data[i].Cases;

                    // Calculate daily new cases (difference from previous day)
                    let dailyNewCases = currentDayCases - previousDayCases;
                    plotDataX.push(originalData.data[i].Date);
                    newCasesY.push(dailyNewCases);
                    cumulativeCasesY.push(currentDayCases);
                }

                // First Graph: Plot the 7-day forecast (new cases)
                var sevenDayForecastPlot = {
                    x: forecastNewCasesX,
                    y: forecastNewCasesY,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: '7-day Forecast (New Cases)',
                    marker: { color: 'red' },
                    line: { shape: 'linear' }
                };

                Plotly.newPlot('forecast-plot', [sevenDayForecastPlot], {
                    title: 'Forecasted New COVID-19 Cases (7 Days)',
                    xaxis: { title: 'Date' },
                    yaxis: { title: 'New Cases' },
                    showlegend: true
                });

                // Second Graph: Plot original and forecasted new cases together
                var originalNewCasesPlotData = {
                    x: plotDataX,
                    y: newCasesY,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Original New Cases',
                    line: { color: 'blue' }
                };

                var forecastNewCasesPlotData = {
                    x: forecastNewCasesX,
                    y: forecastNewCasesY,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Forecasted New Cases',
                    line: { color: 'red' }
                };

                Plotly.newPlot('forecast-plot-new-cases', [originalNewCasesPlotData, forecastNewCasesPlotData], {
                    title: 'Original & Forecasted New Cases Over Time (Daily)',
                    xaxis: { title: 'Date' },
                    yaxis: { title: 'New Cases' }
                });

                // Third Graph: Plot original and forecasted cumulative cases together
                var originalCumulativePlotData = {
                    x: plotDataX,
                    y: cumulativeCasesY,
                    type: 'scatter',
                    mode: 'lines',
                    name: 'Original Cumulative Cases',
                    line: { color: 'blue' }
                };

                var forecastCumulativePlotData = {
                    x: forecastCumulativeX,
                    y: forecastCumulativeY,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Forecasted Cumulative Cases',
                    line: { color: 'red' }
                };

                Plotly.newPlot('forecast-plot-cumulative-cases', [originalCumulativePlotData, forecastCumulativePlotData], {
                    title: 'Cumulative COVID-19 Cases Over Time',
                    xaxis: { title: 'Date' },
                    yaxis: { title: 'Total Cases' }
                });
                // Automatically download CSV and PNG after rendering the graph
                downloadCSV();
                downloadPNG();
                downloadTxt();
            })
            .catch(error => console.error('Error fetching original data:', error));
    })
    .catch(error => console.error('Error fetching forecast data:', error));
