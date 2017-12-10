$(document).ready(function() {

    var deleteImage$ = (function() {

        var modal = $('#deleteImageModal');

        modal.on('show.bs.modal', function (e) {
            var imageId = $(e.relatedTarget).data('image-id');
            modal.data('image-id', imageId);
        });

        modal.on('click', '.btn-primary', function (e) {
            modal.modal('hide');
        });

        return Rx.Observable.create(function(observer) {
            modal.on('click', '.btn-primary', function (e) {
                var imageId = modal.data('image-id');
                observer.next(imageId);
            });
        });
    }());

    deleteImage$.mergeMap(deleteImage).subscribe(reload);

    function deleteImage(imageId) {
        return Rx.Observable.fromPromise($.ajax({
            url: '/api/image/' + imageId,
            method: 'DELETE'
        }));
    }

    function reload() {
        window.location = window.location;
    }
});