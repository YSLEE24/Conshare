// ✅ 페이지의 HTML이 모두 로딩된 후 실행되도록 보장
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

            // 필수값 유효성 검사
            if (!number || !available_from || !price || !tare || !size) {
                $.toast({
                    heading: "입력 오류!",
                    text: "필수 항목을 모두 입력해 주세요.",
                    showHideTransition: "fade",
                    icon: "warning",
                    position: "top-right"
                });
                return;
            }

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
            .then(response => response.json())
            .then(data => {
                $.toast({
                    heading: "성공!",
                    text: data.message || "컨테이너가 성공적으로 등록되었습니다.",
                    showHideTransition: "slide",
                    icon: "success",
                    position: "top-right"
                });

                const form = document.getElementById("container-form");
                if (form) form.reset();
            })
            .catch(error => {
                console.error("에러 발생:", error);
                $.toast({
                    heading: "에러!",
                    text: "등록 중 문제가 발생했습니다.",
                    showHideTransition: "fade",
                    icon: "error",
                    position: "top-right"
                });
            });
        });
    }
});
