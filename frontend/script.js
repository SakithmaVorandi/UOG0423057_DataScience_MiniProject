// ============================================================
// STUDENT PERFORMANCE PREDICTION
// ============================================================


// Get the prediction form.

const form = document.getElementById(
    "predictionForm"
);


// Listen for form submission.

form.addEventListener(
    "submit",
    async function(event) {

        // Prevent the browser from refreshing the page.

        event.preventDefault();


        // ====================================================
        // GET USER INPUT
        // ====================================================

        const studentData = {

            gender:
                document.getElementById(
                    "gender"
                ).value,

            race_ethnicity:
                document.getElementById(
                    "race_ethnicity"
                ).value,

            parental_education:
                document.getElementById(
                    "parental_education"
                ).value,

            lunch:
                document.getElementById(
                    "lunch"
                ).value,

            test_preparation:
                document.getElementById(
                    "test_preparation"
                ).value
        };


        try {

            // =================================================
            // SEND DATA TO FASTAPI
            // =================================================

            const response = await fetch(
                "http://127.0.0.1:8000/predict",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        studentData
                    )
                }
            );


            // Convert API response to JSON.

            const result =
                await response.json();


            // =================================================
            // DISPLAY RESULT
            // =================================================

            document.getElementById(
                "prediction"
            ).textContent =
                result.prediction;


            document.getElementById(
                "passProbability"
            ).textContent =
                (
                    result.probabilities.Pass * 100
                ).toFixed(2) + "%";

            document.getElementById(
                "improvementProbability"
            ).textContent =
                (
                    result.probabilities[
                        "Needs Improvement"
                    ] * 100
                ).toFixed(2) + "%";


            // Show the result section.

            document.getElementById(
                "result"
            ).classList.remove(
                "hidden"
            );


        } catch (error) {

            console.error(
                "Error:",
                error
            );

            alert(
                "Unable to connect to the prediction server."
            );
        }

    }
);