function validateForm() {

    // Check if the Book Author is not empty
    var bookAuthor = document.getElementById("bookAuthor").value;
    if (bookAuthor.trim() === "") {
        alert("Please enter the Book Author.");
        return false;
    }

    // Check if the Publish Year is a valid number
    var publishYear = document.getElementById("publishYear").value;
    if (isNaN(publishYear) || publishYear <= 0) {
        alert("Please enter a valid Publish Year.");
        return false;
    }

    // Check if a Genre option is selected
    var genre = document.getElementById("genre").value;
    if (genre === "") {
        alert("Please select a Genre.");
        return false;
    }

    // Check if a Category option is selected
    var category = document.getElementById("category").value;
    if (category === "") {
        alert("Please select a Category.");
        return false;
    }
// Check if an image is selected
var imageFile = document.getElementById("image").files[0];
if (!imageFile) {
    alert("Please select an image.");
    return false;
}

// Check if a file is selected
var file = document.getElementById("file").files[0];
if (!file) {
    alert("Please select a file.");
    return false;
}

 // Check image file constraints
var imageFile = document.getElementById("image").files[0];
if (imageFile) {
    var allowedImageTypes = ["image/jpeg", "image/png", "image/gif"];
    var maxImageSize = 2097152; // 2MB in bytes
    if (!allowedImageTypes.includes(imageFile.type)) {
        alert("Error: Only JPEG, PNG, and GIF files are allowed for images.");
        return false;
    }
    if (imageFile.size > maxImageSize) {
        alert("Error: The image file size exceeds the allowed limit (2MB).");
        return false;
    }
}
    // You can add more validations here as needed

    return true; // If all validations pass, the form can be submitted
}