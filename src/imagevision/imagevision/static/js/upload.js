$(document).ready(function(){

    handleSubmit();

    function handleSubmit() {
        $('#upload').on('submit', function (e) {
            $('#waitModal').modal('show');
        });
    }
});