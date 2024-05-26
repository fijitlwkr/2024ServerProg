document.addEventListener('DOMContentLoaded', () => {
    const joinBtn = document.getElementById('join-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    joinBtn.addEventListener('click', () => {
        alert('그룹에 가입했습니다.');
        // 실제 가입 처리 로직을 여기에 추가하세요.
    });

    cancelBtn.addEventListener('click', () => {
        window.location.href = 'home.html';
    });
});
