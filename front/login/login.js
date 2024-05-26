document.addEventListener('DOMContentLoaded', () => {
    const signInBtn = document.getElementById('sign-in-btn');
    const logInBtn = document.getElementById('log-in-btn');

    signInBtn.addEventListener('click', () => {
        window.location.href = 'sign-up.html'; // 회원가입 페이지로 이동
    });

    logInBtn.addEventListener('click', () => {
        const id = document.getElementById('id').value;
        const password = document.getElementById('password').value;

        // 여기에 실제 로그인 검증 로직을 추가합니다.
        // 예를 들어, 서버에 요청을 보내고 응답을 처리합니다.

        if (id === 'testuser' && password === 'testpassword') { // 임시 검증 로직
            alert('로그인 성공');
            window.location.href = 'home.html'; // 홈 페이지로 이동
            // 로그인 상태를 유지하기 위해 쿠키나 로컬 스토리지 등을 사용할 수 있습니다.
        } else {
            alert('ID 또는 비밀번호가 올바르지 않습니다.');
        }
    });
});
