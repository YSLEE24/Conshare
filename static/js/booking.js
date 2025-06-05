// static/js/booking.js
$('.confirm-booking').on('click', function () {
    const containerData = getSelectedContainerInfo();
    fetch('/booking/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(containerData)
    }).then(response => {
        if (response.ok) {
            // Bottom Center 위치로 알림 띄우기
            showNotification('bottom', 'center');

            // 2초 후 리디렉션
            setTimeout(() => {
                window.location.href = "/booked";
            }, 2000);
        } else {
            // 실패한 경우에도 토스트 띄우기 (옵션)
            $.notify({
                icon: "pe-7s-close-circle",
                message: "예약 실패. 다시 시도해주세요."
            }, {
                type: 'danger',
                timer: 2000,
                placement: {
                    from: 'bottom',
                    align: 'center'
                }
            });
        }
    });
});
