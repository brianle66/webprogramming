$(document).ready(function() {
    // Enable inline editing
    $('.edit-post').click(function() {
        const postId = $(this).data('id');
        const contentElement = $(`.post-content[data-id=${postId}]`);
        const currentContent = contentElement.text().trim();
        const newContent = prompt('Edit post:', currentContent);
        
        if (newContent !== null) {
            // Send AJAX request to update post content
            $.ajax({
                url: `/editpost/${postId}`,
                method: 'POST',
                data: {
                    newcontent: newContent,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(response) {
                    // Update UI with new content
                    contentElement.text(newContent);
                },
                error: function(xhr, status, error) {
                    console.error('Error updating post content:', error);
                }
            });
        }
    });

    // Handle new post form submission
    $('#new-post-form').submit(function(event) {
        event.preventDefault();
        const newContent = $('#new-post-content').val().trim();

        if (newContent !== '') {
            // Send AJAX request to create a new post
            $.ajax({
                url: '{% url "newpost" %}',
                method: 'POST',
                data: {
                    content: newContent,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function(response) {
                    // Clear input field and update UI with new post
                    $('#new-post-content').val('');
                    // You may need to dynamically insert the new post into the UI here
                },
                error: function(xhr, status, error) {
                    console.error('Error creating new post:', error);
                }
            });
        }
    });
});
