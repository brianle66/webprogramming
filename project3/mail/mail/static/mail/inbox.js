document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Compose form handler
  document.querySelector('#compose-form').addEventListener('submit', (event) => sent_email(event));

  // By default, load the inbox
  load_mailbox('inbox');
});

// Compose tab view
function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Mailbox tab view
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Show emails in mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(email => {
        // Get the data from email
        const element = document.createElement('div');
        if (mailbox === 'sent') {
          element.innerHTML = `
            <h5>Subject: ${email.subject}</h5>
            <h6>To: ${email.recipients}</h6>
            <h6>Time: ${email.timestamp}</h6>
        `} else {
          element.innerHTML = `
            <h5>Subject: ${email.subject}</h5>
            <h6>From: ${email.sender}</h6>
            <h6>Time: ${email.timestamp}</h6>
        `
        };
        element.className = '';
        element.addEventListener('click', function() {
            // Add class to read email to change BG color
            if (email.read) {
              element.classList.add('read')
            } else {
              element.classList.add('unread')
            }
            console.log('This element has been clicked!')
            
            // Show email content
            view_email(email.id);
            console.log(element.className)
        });
        
        document.querySelector('#emails-view').append(element);
        
      });
      // Print emails
      console.log(emails);

      // ... do something else with emails ...     
  });
}
function view_email(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read : true
    })
  })
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);
    document.querySelector('#email-content').style.display = 'block';
  })
  
}

function sent_email(event) {
  event.preventDefault();
  // Get data from Compose form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  // Store data in DB
  fetch(`/emails`, {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      compose_email();
  });
}