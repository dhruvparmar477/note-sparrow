// document.getElementById("upload-image").addEventListener("change", function(event) {
//     const textarea = document.querySelector(".note-content");
//     const file = event.target.files[0];
//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             const preview = document.getElementById("image-preview");
//             preview.style.backgroundImage = `url(${e.target.result})`;
//             preview.style.display = "block";
//         };
//         reader.readAsDataURL(file);
//     }
//     if (textarea) {
//         textarea.addEventListener("input", function () {
//             this.style.height = "auto";
//             this.style.height = this.scrollHeight + "px";
//         });
//     }
// });




// document.getElementById("upload-image").addEventListener("change", function(event) {
//     const textarea = document.querySelector(".note-content");
//     const preview = document.getElementById("image-preview");
//     const file = event.target.files[0];

//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             preview.style.backgroundImage = `url(${e.target.result})`;
//             preview.style.display = "block";
//             textarea.style.maxWidth = "65%"; // Shrinks when image is uploaded
//         };
//         reader.readAsDataURL(file);
//     } else {
//         preview.style.display = "none";
//         textarea.style.maxWidth = "100%"; // Expands fully when no image
//     }

//     // Auto-expand textarea as user types
//     if (textarea) {
//         textarea.addEventListener("input", function () {
//             this.style.height = "auto";
//             this.style.height = this.scrollHeight + "px";
//         });
//     }
// });


// document.getElementById("upload-image").addEventListener("change", function(event) {
//     const textarea = document.querySelector(".note-content");
//     const file = event.target.files[0];
//     const preview = document.getElementById("image-preview");

//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             preview.style.backgroundImage = `url(${e.target.result})`;
//             preview.style.display = "block"; // Show the image preview
//         };
//         reader.readAsDataURL(file);
//     }

    // Adjust the text area size dynamically
//     if (textarea) {
//         textarea.addEventListener("input", function () {
//             this.style.height = "auto";
//             this.style.height = this.scrollHeight + "px";
//         });
//     }

//     // Resize textarea when no image is uploaded
//     if (!file) {
//         textarea.style.width = "100%"; // Expand textarea fully
//     } else {
//         textarea.style.width = "65%"; // Shrink when image is present
//     }
// });

// Image Zoom Effect
// document.getElementById("image-preview").addEventListener("click", function () {
//     const zoomedContainer = document.createElement("div");
//     zoomedContainer.classList.add("zoomed-image-container");

//     const zoomedImage = document.createElement("div");
//     zoomedImage.classList.add("zoomed-image");
//     zoomedImage.style.backgroundImage = this.style.backgroundImage;

//     zoomedContainer.appendChild(zoomedImage);
//     document.body.appendChild(zoomedContainer);

//     // Close zoom on click outside
//     zoomedContainer.addEventListener("click", function () {
//         zoomedContainer.classList.add("fade-out");
//         setTimeout(() => document.body.removeChild(zoomedContainer), 300);
//     });
// });
