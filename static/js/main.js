$(document).ready(function() {
  // Get the form element and input element
  var form = $('#upload-form');
  var input = $('#upload-input');

  // On form submit
  form.submit(function(event) {
    // Prevent default form submission
    event.preventDefault();

    // Get the file input
    var fileInput = input[0].files[0];

    // Create a FormData object and add the file input to it
    var formData = new FormData();
    formData.append('file', fileInput);

    // Display the loading spinner
    $('.loading-spinner').show();

    // Send an AJAX request to the server to process the uploaded image
    $.ajax({
      url: '/predict',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        // Hide the loading spinner
        $('.loading-spinner').hide();

        // Display the result
        $('.result-text').text('Detected disease: ' + response.result);

        // Get the search query for the detected disease
        var searchQuery = 'How to treat ' + response.result + ' disease';

        // Create a Google search URL with the search query
        var searchUrl = 'https://www.google.com/search?q=' + encodeURIComponent(searchQuery);

        // Display the control methods section
        $('.control-methods').show();

        // Set the search URL as the href of the control methods link
        $('.control-methods a').attr('href', searchUrl);
      },
      error: function(xhr, status, error) {
        // Hide the loading spinner
        $('.loading-spinner').hide();

        // Display an error message
        $('.result-text').text('Error: ' + error);
      }
    });
  });
});
