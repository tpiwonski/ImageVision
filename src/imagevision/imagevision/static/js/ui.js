$(document).ready(function() {

    createDeleteObservable().
        mergeMap(deleteImage).
        subscribe(reloadPage);

    dismissAlerts();

    function createDeleteObservable() {
        var modal = $('#deleteImageModal');

        modal.on('show.bs.modal', function (e) {
            var imageId = $(e.relatedTarget).data('image-id');
            modal.data('image-id', imageId);
        });

        modal.on('click', '#deleteImageButton', function (e) {
            modal.modal('hide');
        });

        return Rx.Observable.create(function(observer) {
            modal.on('click', '#deleteImageButton', function (e) {
                var imageId = modal.data('image-id');
                observer.next(imageId);
            });
        });
    }

    function deleteImage(imageId) {
        return Rx.Observable.fromPromise($.ajax({
            url: '/ajax/image/' + imageId,
            method: 'DELETE'
        }));
    }

    function reloadPage() {
        window.location = window.location;
    }

    function dismissAlerts() {
        Rx.Observable.timer(2000).
            subscribe(function(){
                $('.alert').slideUp('slow');
            });
    }
});