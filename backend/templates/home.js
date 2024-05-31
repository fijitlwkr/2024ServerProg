document.addEventListener('DOMContentLoaded', () => {
    const blocks = document.querySelectorAll('.block');
    const profileBtn = document.getElementById('profile-btn');

    blocks.forEach(block => {
        block.addEventListener('click', () => {
            const target = block.getAttribute('data-target');
            if (target) {
                window.location.href = target;
            }
        });
    });

    profileBtn.addEventListener('click', () => {
        window.location.href = 'profile.html'; // 프로필 페이지로 이동
    });
});
