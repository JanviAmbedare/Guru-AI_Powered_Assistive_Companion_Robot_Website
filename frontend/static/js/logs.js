document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadLogs();

    }
);


async function loadLogs(){

    try{

        const response =
            await apiRequest(
                "GET",
                `/conversations/${USER_ID}`
            );

        renderLogs(
            response.history || []
        );

    }

    catch(error){

        console.error(
            error
        );
    }
}


function renderLogs(
    logs
){

    const table =
        document.getElementById(
            "logsTableBody"
        );

    table.innerHTML = "";

    logs.forEach(
        log => {

            table.innerHTML += `

                <tr>

                    <td>
                        ${
                            log.timestamp || "-"
                        }
                    </td>

                    <td>
                        ${
                            log.intent || "-"
                        }
                    </td>

                    <td>
                        ${
                            log.emotion || "-"
                        }
                    </td>

                    <td>
                        ${
                            log.user_input || "-"
                        }
                    </td>

                    <td>
                        ${
                            log.response_text || "-"
                        }
                    </td>

                </tr>
            `;
        }
    );
}