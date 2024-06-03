document.addEventListener('DOMContentLoaded', function() {
    const projectNameElement = document.querySelector("#projectName");
    const projectCodeElement = document.querySelector("#projectCode");
    const projectDateElement = document.querySelector("#projectDate");
    const projectCustomerElement = document.querySelector("#projectCustomer");

    const initialData = {
        name: projectNameElement.innerText,
        code: projectCodeElement.innerText,
        date: projectDateElement.innerText,
        customer: projectCustomerElement.innerText
    };

    document.querySelector('#edit_project').addEventListener('click', edit_project);
    document.querySelector('#cancel_edit').addEventListener('click', cancel_edit);
    document.querySelector('#save_project').addEventListener('click', save_project);

    function edit_project() {
        document.querySelector('#save_project').style.display = 'inline-block';
        document.querySelector('#cancel_edit').style.display = 'inline-block';
        document.querySelector('#edit_project').style.display = 'none';

        projectNameElement.innerHTML = `<input type="text" id="projectNameInput" value="${initialData.name}">`;
        projectCodeElement.innerHTML = `<input type="text" id="projectCodeInput" value="${initialData.code}">`;
        projectDateElement.innerHTML = `<input type="text" id="projectDateInput" value="${initialData.date}">`;
        projectCustomerElement.innerHTML = `<input type="text" id="projectCustomerInput" value="${initialData.customer}">`;
    }

    function cancel_edit() {
        projectNameElement.innerHTML = initialData.name;
        projectCodeElement.innerHTML = initialData.code;
        projectDateElement.innerHTML = initialData.date;
        projectCustomerElement.innerHTML = initialData.customer;

        document.querySelector('#save_project').style.display = 'none';
        document.querySelector('#cancel_edit').style.display = 'none';
        document.querySelector('#edit_project').style.display = 'inline-block';
    }

    function save_project() {
        const projectNameInput = document.querySelector("#projectNameInput").value;
        const projectCodeInput = document.querySelector("#projectCodeInput").value;
        const projectDateInput = document.querySelector("#projectDateInput").value;
        const projectCustomerInput = document.querySelector("#projectCustomerInput").value;

        fetch('/update_project/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                name: projectNameInput,
                code: projectCodeInput,
                date: projectDateInput,
                customer: projectCustomerInput
            })
        }).then(response => {
            return response.json().then(data => {
                if (response.ok) {
                    projectNameElement.innerText = projectNameInput;
                    projectCodeElement.innerText = projectCodeInput;
                    projectDateElement.innerText = projectDateInput;
                    projectCustomerElement.innerText = projectCustomerInput;

                    document.querySelector('#save_project').style.display = 'none';
                    document.querySelector('#cancel_edit').style.display = 'none';
                    document.querySelector('#edit_project').style.display = 'inline-block';
                } else {
                    console.error('Failed to update project:', data);
                    alert('Failed to update project');
                }
            });
        }).catch(error => {
            console.error('Error:', error);
            alert('Failed to update project');
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
