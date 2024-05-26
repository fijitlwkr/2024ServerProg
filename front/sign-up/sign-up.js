document.addEventListener('DOMContentLoaded', () => {
    const joinUsBtn = document.getElementById('join-us-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    joinUsBtn.addEventListener('click', () => {
        const id = document.getElementById('id').value;
        const password = document.getElementById('password').value;
        const nickname = document.getElementById('nickname').value;
        const introduction = document.getElementById('introduction').value;

        // 여기에 회원가입 데이터를 서버에 전송하는 로직을 추가하세요.
        // 예를 들어, AJAX 또는 Fetch API를 사용하여 서버에 데이터 전송
        const userData = { id, password, nickname, introduction };

        fetch('/api/sign-up', { // 예시 URL, 실제 서버 URL로 대체하세요.
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('회원가입 성공');
                window.location.href = 'login.html'; // 로그인 페이지로 이동
            } else {
                alert('회원가입 실패: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('회원가입 중 오류가 발생했습니다.');
        });
    });

    cancelBtn.addEventListener('click', () => {
        window.location.href = 'login.html'; // 로그인 페이지로 이동
    });
});
