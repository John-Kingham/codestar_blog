/**
 * Add event listeners to handle Edit Comment button clicks.
 *
 * The event handler sets the comment text box's text to the text of the
 * selected comment, and updates the form to send data to the edit comment view.
 */
function addEditEventListeners() {
    const editButtons = document.getElementsByClassName("btn-edit");
    const commentTextField = document.getElementById("id_body");
    const commentForm = document.getElementById("commentForm");
    const submitButton = document.getElementById("submitButton");
    for (const editButton of editButtons) {
        editButton.addEventListener("click", function (e) {
            const commentId = e.target.getAttribute("comment_id");
            const commentText = document.getElementById(
                `comment${commentId}`
            ).innerText;
            commentTextField.value = commentText;
            submitButton.innerText = "Update";
            commentForm.setAttribute("action", `edit_comment/${commentId}`);
        });
    }
}

/**
 * Add event listeners to handle Delete Comment button clicks.
 *
 * The event handler updates the delete modal's button so the selected
 * comment's ID is sent to the delete comment view.
 */
function addDeleteEventListeners() {
    const deleteConfirmModal = new bootstrap.Modal(
        document.getElementById("deleteModal")
    );
    const deleteBtns = document.getElementsByClassName("btn-delete");
    const confirmDeleteBtn = document.getElementById("deleteConfirm");
    for (const deleteBtn of deleteBtns) {
        deleteBtn.addEventListener("click", function (e) {
            const commentId = e.target.getAttribute("comment_id");
            confirmDeleteBtn.href = `delete_comment/${commentId}`;
            deleteConfirmModal.show();
        });
    }
}

addEditEventListeners();
addDeleteEventListeners();
