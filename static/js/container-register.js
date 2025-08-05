document.addEventListener("DOMContentLoaded", function () {
    const registerButton = document.getElementById("register-btn");

    if (registerButton) {
        registerButton.addEventListener("click", function (event) {
            event.preventDefault();

            const number = document.getElementById("container_number").value;
            const size = document.getElementById("container_size").value;
            const available_from = document.getElementById("startDate").value;
            const endDateInputVal = document.getElementById("endDate").value;
            const available_to = endDateInputVal !== "" ? endDateInputVal : null;
            const price = document.getElementById("price").value;
            const tare = document.getElementById("tare_weight").value;
            const remarks = document.getElementById("remarks").value;
            const releaseRef = document.getElementById("release_ref")?.value || "";

            // ✅ 필수 입력 체크
            if (!number || !available_from || !price || !tare || !size) {
                const alertModal = document.getElementById("alertModal");
                const alertModalBody = alertModal.querySelector(".modal-body");
                alertModalBody.textContent = "필수 항목을 모두 입력해주세요.";
                $('#alertModal').modal('show');
                return;
            }

            // ✅ 서버에 데이터 전송
            fetch("/register/submit", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    container_number: number,
                    size: size,
                    available_from: available_from,
                    available_to: available_to,
                    price: price,
                    tare: tare,
                    remarks: remarks,
                    release_ref: releaseRef
                })
            })
            .then(response => {
                if (!response.ok) throw new Error("서버 응답 오류");
                return response.json();
            })
            .then(data => {
                // 성공 모달 표시
                document.getElementById("successMessage").innerText = data.message || '성공적으로 등록되었습니다.';
                $('#successModal').modal('show');  // ← jQuery로 모달 트리거
                const form = document.getElementById("container-form");
                if (form) form.reset();
            })
            .catch(error => {
                console.error("에러 발생:", error);
                document.getElementById("errorMessage").innerText = '등록 중 문제가 발생했습니다. 다시 시도해주세요.';
                $('#errorModal').modal('show');
            });
        });
    }
});


// document.addEventListener("DOMContentLoaded", function () {
//     const registerButton = document.getElementById("register-btn");

//     if (registerButton) {
//         registerButton.addEventListener("click", function (event) {
//             event.preventDefault();

//             const number = document.getElementById("container_number").value;
//             const size = document.getElementById("container_size").value;
//             const available_from = document.getElementById("startDate").value;
//             const endDateInputVal = document.getElementById("endDate").value;
//             const available_to = endDateInputVal !== "" ? endDateInputVal : null;
//             const price = document.getElementById("price").value;
//             const tare = document.getElementById("tare_weight").value;
//             const remarks = document.getElementById("remarks").value;
//             const releaseRef = document.getElementById("release_ref")?.value || "";

//             // ✅ 필수 입력 체크
//             if (!number || !available_from || !price || !tare || !size) {
//                 Swal.fire({
//                     icon: 'warning',
//                     title: '⚠️ 입력 오류',
//                     text: '필수 항목을 모두 입력해주세요.',
//                     confirmButtonText: '확인'
//                 });
//                 return;
//             }

//             // ✅ 서버에 데이터 전송
//             fetch("/register/submit", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({
//                     container_number: number,
//                     size: size,
//                     available_from: available_from,
//                     available_to: available_to,
//                     price: price,
//                     tare: tare,
//                     remarks: remarks,
//                     release_ref: releaseRef
//                 })
//             })
//             .then(response => {
//                 if (!response.ok) throw new Error("서버 응답 오류");
//                 return response.json();
//             })
//             .then(data => {
//                 Swal.fire({
//                 icon: 'success',
//                 title: '등록 완료',
//                 text: data.message || '성공적으로 등록되었습니다.',
//                 confirmButtonText: '확인',
//                 allowOutsideClick: false,
//                 allowEscapeKey: false
//                 }).then(() => {
//                 const form = document.getElementById("container-form");
//                 if (form) form.reset();
//                 });
//             })
//             .catch(error => {
//                 console.error("에러 발생:", error);
//                 Swal.fire({
//                     icon: 'error',
//                     title: '오류 발생',
//                     text: '등록 중 문제가 발생했습니다. 다시 시도해주세요.',
//                     confirmButtonText: '확인'
//                 });
//             });
//         });
//     }
// });
