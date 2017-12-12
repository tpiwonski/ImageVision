$(document).ready(function() {

    loadImage().
        mergeMap(function(image) {
            return Rx.Observable.concat(Rx.Observable.of(image), windowResized().map(function() {
                return image;
            }))
        }).
        withLatestFrom(getAnnotations()).
        subscribe(drawAnnotations);

    function windowResized() {
        return Rx.Observable.fromEvent(window, 'resize');
    }

    function loadImage() {
        var image = $('#image');
        var loaded$ = Rx.Observable.fromEvent(image, 'load').map(function(e) {
            return e.target;
        });
        image.attr('src', image.data('src'));
        return loaded$;
    }

    function getAnnotations() {
        return Rx.Observable.of(JSON.parse($('#annotations').text()))
    }

    function drawAnnotations(args) {
        var image = args[0];
        var annotations = args[1];

        var canvas = document.getElementById('canvas');

        canvas.style.top = image.offsetTop + 'px';
        canvas.style.left = image.offsetLeft + 'px';
        canvas.width = image.width;
        canvas.height = image.height;

        var scaleX = image.width / image.naturalWidth;
        var scaleY = image.height / image.naturalHeight;

        var ctx = canvas.getContext('2d');
        ctx.strokeStyle="#00FF00";

        annotations['face_annotations'].forEach(function(face) {
            var v = face['bounding_poly']['vertices'];
            var x = v[0]['x'];
            var y = v[0]['y'];
            var w = v[1]['x'] - v[0]['x'];
            var h = v[2]['y'] - v[1]['y'];

            ctx.strokeRect(x * scaleX, y * scaleY, w * scaleX, h * scaleY);

            face['landmarks'].forEach(function(landmark) {
                var position = landmark['position'];

                var x = position['x'];
                var y = position['y'];

                ctx.strokeRect(x * scaleX, y * scaleY, 1, 2);
            });
        });
    }
});