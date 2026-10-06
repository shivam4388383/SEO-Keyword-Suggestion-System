// ==========================================
// SENTIMENT CHART INSTANCE
// ==========================================

let sentimentChart = null;


// ==========================================
// ANALYZE KEYWORD
// ==========================================

async function analyzeKeyword() {

    const input =
        document.getElementById("keywordInput");

    const errorMessage =
        document.getElementById("errorMessage");

    const results =
        document.getElementById("results");


    const keyword =
        input.value.trim();


    errorMessage.textContent = "";


    // --------------------------------------
    // EMPTY INPUT
    // --------------------------------------

    if (!keyword) {

        errorMessage.textContent =
            "Please enter a keyword.";

        results.classList.add(
            "hidden"
        );

        return;
    }


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        keyword: keyword
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );
        }


        displayResults(data);

        loadHistory();


    } catch (error) {

        errorMessage.textContent =
            error.message;

        results.classList.add(
            "hidden"
        );

        console.error(
            "Analysis Error:",
            error
        );
    }
}


// ==========================================
// DISPLAY RESULTS
// ==========================================

function displayResults(data) {

    const results =
        document.getElementById(
            "results"
        );


    const table =
        document.getElementById(
            "keywordTable"
        );


    // --------------------------------------
    // KEYWORD SUGGESTIONS
    // --------------------------------------

    table.innerHTML = "";


    if (
        data.suggestions &&
        Array.isArray(
            data.suggestions
        )
    ) {

        data.suggestions.forEach(
            item => {

                const row =
                    document.createElement(
                        "tr"
                    );


                const keywordCell =
                    document.createElement(
                        "td"
                    );

                keywordCell.textContent =
                    item.keyword;


                const wordCountCell =
                    document.createElement(
                        "td"
                    );

                wordCountCell.textContent =
                    item.word_count;


                // Semantic Score column
const semanticScoreCell =
    document.createElement("td");

semanticScoreCell.textContent =
    `${item.semantic_score ?? 0}%`;


// Estimated Score column
const scoreCell =
    document.createElement("td");

scoreCell.textContent =
    item.score;


// Add cells in correct order
row.appendChild(keywordCell);
row.appendChild(wordCountCell);
row.appendChild(semanticScoreCell);
row.appendChild(scoreCell);


                table.appendChild(
                    row
                );
            }
        );
    }


    // --------------------------------------
    // SENTIMENT
    // --------------------------------------

    const sentiment =
        data.sentiment || {};


    const positive =
        Number(
            sentiment.Positive
        ) || 0;


    const neutral =
        Number(
            sentiment.Neutral
        ) || 0;


    const negative =
        Number(
            sentiment.Negative
        ) || 0;


    const positiveElement =
        document.getElementById(
            "positive"
        );


    const neutralElement =
        document.getElementById(
            "neutral"
        );


    const negativeElement =
        document.getElementById(
            "negative"
        );


    if (positiveElement) {

        positiveElement.textContent =
            `${positive}%`;
    }


    if (neutralElement) {

        neutralElement.textContent =
            `${neutral}%`;
    }


    if (negativeElement) {

        negativeElement.textContent =
            `${negative}%`;
    }


    // --------------------------------------
    // SENTIMENT SOURCE
    // --------------------------------------

    const sentimentSource =
        document.getElementById(
            "sentimentSource"
        );


    if (sentimentSource) {

        if (data.sentiment_source) {

            sentimentSource.textContent =
                `Source: ${data.sentiment_source}`;

        } else {

            sentimentSource.textContent =
                "";
        }
    }


    // --------------------------------------
    // SENTIMENT CHART
    // --------------------------------------

    const chartCanvas =
        document.getElementById(
            "sentimentChart"
        );


    if (chartCanvas) {

        if (sentimentChart) {

            sentimentChart.destroy();

            sentimentChart = null;
        }


        sentimentChart =
            new Chart(
                chartCanvas,
                {
                    type: "doughnut",

                    data: {

                        labels: [
                            "Positive",
                            "Neutral",
                            "Negative"
                        ],

                        datasets: [
                            {
                                data: [
                                    positive,
                                    neutral,
                                    negative
                                ],

                                backgroundColor: [
                                    "#10b981",
                                    "#f59e0b",
                                    "#f43f5e"
                                ],

                                borderWidth: 0,

                                hoverOffset: 4
                            }
                        ]
                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio:
                            false,

                        plugins: {

                            legend: {

                                position:
                                    "bottom",

                                labels: {

                                    color:
                                        "#94a3b8",

                                    font: {
                                        size: 11
                                    },

                                    padding: 15
                                }
                            }
                        },

                        cutout: "70%"
                    }
                }
            );
    }


    // --------------------------------------
    // RECOMMENDATION
    // --------------------------------------

    const recommendedKeyword =
        document.getElementById(
            "recommendedKeyword"
        );


    const recommendationScore =
        document.getElementById(
            "recommendationScore"
        );


    if (
        recommendedKeyword &&
        recommendationScore
    ) {

        if (data.recommendation) {

            recommendedKeyword.textContent =
                data.recommendation.keyword;


            recommendationScore.textContent =
                `Estimated Score: ${data.recommendation.score}`;

        } else {

            recommendedKeyword.textContent =
                "No recommendation available";


            recommendationScore.textContent =
                "";
        }
    }


    // --------------------------------------
    // SHOW RESULTS
    // --------------------------------------

    results.classList.remove(
        "hidden"
    );
}


// ==========================================
// LOAD SEARCH HISTORY
// ==========================================

async function loadHistory() {

    const historyTable =
        document.getElementById(
            "historyTable"
        );


    if (!historyTable) {
        return;
    }


    try {

        const response =
            await fetch(
                "http://127.0.0.1:5000/history"
            );


        if (!response.ok) {

            throw new Error(
                "Unable to load search history."
            );
        }


        const history =
            await response.json();


        historyTable.innerHTML =
            "";


        if (
            Array.isArray(history) &&
            history.length > 0
        ) {

            history.forEach(
                item => {

                    const row =
                        document.createElement(
                            "tr"
                        );


                    const keywordCell =
                        document.createElement(
                            "td"
                        );

                    keywordCell.textContent =
                        item.keyword;


                    const scoreCell =
                        document.createElement(
                            "td"
                        );

                    scoreCell.textContent =
                        item.score;


                    const dateCell =
                        document.createElement(
                            "td"
                        );

                    dateCell.textContent =
                        item.searched_at;


                    row.appendChild(
                        keywordCell
                    );

                    row.appendChild(
                        scoreCell
                    );

                    row.appendChild(
                        dateCell
                    );


                    historyTable.appendChild(
                        row
                    );
                }
            );

        } else {

            const row =
                document.createElement(
                    "tr"
                );


            const cell =
                document.createElement(
                    "td"
                );


            cell.colSpan = 3;

            cell.textContent =
                "No search history available.";


            row.appendChild(
                cell
            );


            historyTable.appendChild(
                row
            );
        }


    } catch (error) {

        console.error(
            "Failed to load search history:",
            error
        );
    }
}


// ==========================================
// LOAD HISTORY ON PAGE LOAD
// ==========================================

loadHistory();