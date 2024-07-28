
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.button').forEach(function(button) {
        button.addEventListener('click', async function() {
            const appointmentId = this.getAttribute('data-appointment-id');
            const status = this.getAttribute('data-status');

            try {
                const response = await postData('set_appointment_status/', {
                    'appointment_id': appointmentId,
                    'status': status
                });



                if (response.success) {
                    logInfo(`Статус обновлен`, false, 2000)
                    location.reload();
                } else {
                    logInfo('Error: ' + response.error, true);
                }
            } catch (error) {
                alert('AJAX error: ' + error.message);
                logInfo('AJAX error: ' + error.message, true);
            }
        });
    });
});