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
function compose_email(email=null) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-content').style.display = 'none';

  // Clear out composition fields
  if (email) {
    // If it's a reply, pre-fill the composition fields with the reply data
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `<type reply here>
    
    On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
  } else {
    // If it's a new email, clear all fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
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
        element.className = 'list-group-item';
        // Add class to read email to change BG color
        if (email.read) {
          element.classList.add('read')
        } else {
          element.classList.add('unread')
        }
        element.addEventListener('click', function() {
            // Show email content
            view_email(email.id);
            console.log(element.className)
            console.log('This element has been clicked!')
        });
        
        document.querySelector('#emails-view').append(element);
        
      });
      // Print emails
      console.log(emails);

      // ... do something else with emails ...     
  });
}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email)
    
    // Update UI to display email content
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-content').style.display = 'block';
    document.querySelector('#email-content').innerHTML = `
      <ul class="list-group list-group-flush">
        <li class="list-group-item"><h5 class="mb-1">Subject: ${email.subject}</h5></li>
        <li class="list-group-item"><h6 class="mb-1">From: ${email.sender}</h6></li>
        <li class="list-group-item"><h6 class="mb-1">To: ${email.recipients.join(', ')}</h6></li>
        <li class="list-group-item"><p class="mb-1">Time: ${email.timestamp}</p></li>
        <li class="list-group-item"><p class="mb-1">${email.body}</p></li>
      </ul>
    `;
    if(!email.read){
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read : true
        })
      })
    }
    //archive btn
    const archive_btn = document.createElement('button');
    archive_btn.className = 'btn';
    archive_btn.innerHTML = email.archived ? 'Unarchive' : 'Archive';
    archive_btn.classList.toggle('btn-primary', !email.archived);
    archive_btn.classList.toggle('btn-warning', email.archived);
    document.querySelector('#email-content').append(archive_btn);
    archive_btn.addEventListener('click', () => archive_email(email.id));
    //reply btn
    const reply_btn = document.createElement('button');
    reply_btn.className = 'btn btn-success';
    reply_btn.innerHTML = 'Reply';
    document.querySelector('#email-content').append(reply_btn);
    reply_btn.addEventListener('click', () => compose_email(email));
  })
}

function archive_email(id){
  fetch(`/emails/${id}`)
  .then (response => response.json())
  .then (email => {
    const newArchivedValue = !email.archived;
    return fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: newArchivedValue
        })
    });
  })
  .then(() => {
    console.log('Email is archived/unarchived');
    // Reload the current page
    window.location.reload();
  })
}
  

function sent_email(event,email) {
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