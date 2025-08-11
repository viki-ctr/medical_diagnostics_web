document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('id_appointment_date');
    if (dateInput) {
        dateInput.addEventListener('change', updateTimeSlots);
    }

    function updateTimeSlots() {
        const doctorId = document.getElementById('id_doctor').value;
        const serviceId = document.getElementById('id_service').value;
        const date = this.value;

        if (doctorId && serviceId && date) {
            fetch(`/appointments/available-slots/?doctor=${doctorId}&service=${serviceId}&date=${date}`)
                .then(response => response.json())
                .then(slots => {
                    const slotsContainer = document.getElementById('time-slots');
                    slotsContainer.innerHTML = slots.map(slot => `
                        <div class="time-slot" data-time="${slot}">
                            ${slot}
                        </div>
                    `).join('');
                });
        }
    }
});
