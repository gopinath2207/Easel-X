// Handle profile image preview and deletion
document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const profileImage = document.getElementById('profileImage');
    const profilePreview = document.querySelector('.profile-preview');
    let defaultImageUrl = '/static/images/default_profile.svg';

    // Add delete button
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.className = 'delete-profile-image';
    deleteButton.innerHTML = '❌';
    deleteButton.style.cssText = `
        position: absolute;
        top: 5px;
        right: 5px;
        background: rgba(255, 0, 0, 0.8);
        color: white;
        border: none;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        cursor: pointer;
        display: none;
        z-index: 2;
    `;
    profilePreview.appendChild(deleteButton);

    // Show delete button if there's an existing image
    if (profileImage.src && !profileImage.src.includes('default_profile.png')) {
        deleteButton.style.display = 'block';
    }

    // Handle file selection
    imageUpload.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profileImage.src = e.target.result;
                deleteButton.style.display = 'block';
                
                // Force browser to show new image by adding timestamp
                profileImage.style.cssText = `
                    max-width: 100%;
                    max-height: 100%;
                    width: auto;
                    height: auto;
                    object-fit: cover;
                    display: block;
                `;
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle delete button click
    deleteButton.addEventListener('click', function() {
        // Clear the file input
        imageUpload.value = '';
        
        // Reset to default image or previous image
        profileImage.src = '/static/default_profile.png';
        deleteButton.style.display = 'none';

        // Add a hidden input to signal image deletion to server
        const deleteFlag = document.createElement('input');
        deleteFlag.type = 'hidden';
        deleteFlag.name = 'remove_profile_picture';
        deleteFlag.value = '1';
        document.getElementById('editProfileForm').appendChild(deleteFlag);
    });
});