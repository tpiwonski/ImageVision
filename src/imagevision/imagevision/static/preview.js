$(document).ready(function() {

    drawAnnotations();

    function drawAnnotations() {
        var face_annotations = JSON.parse($('#annotations').text());

        var img = document.getElementById('image');
        img.onload = function() {
            var canvas = document.getElementById('canvas');

            var scaleX = canvas.width / img.naturalWidth;
            var scaleY = canvas.height / img.naturalHeight;

            var ctx = canvas.getContext('2d');
            ctx.strokeStyle="#00FF00";

            face_annotations.forEach(function(face) {
                var v = face['bounding_poly']['vertices'];
                var x = v[0]['x'];
                var y = v[0]['y'];
                var w = v[1]['x'] - v[0]['x'];
                var h = v[2]['y'] - v[1]['y'];

                ctx.strokeRect(x * scaleX, y * scaleY, w * scaleX, h * scaleY);
            });
        };
        img.src = $(img).data('src');
    };
});