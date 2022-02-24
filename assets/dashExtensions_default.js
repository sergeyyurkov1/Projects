window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng, context) {
                var marker_ = L.icon({
                    iconUrl: "https://dash-leaflet.herokuapp.com/assets/icon_plane.png",
                });
                var true_track = feature.properties.true_track;
                return L.marker(latlng, {
                    icon: marker_,
                    rotationAngle: true_track
                });
            }

            ,
        function1: function(feature, latlng, context) {
            const count = feature.properties.point_count;
            const size =
                count <= 5 ? 'small' :
                count > 5 && count < 10 ? 'medium' : 'large';
            const icon = L.divIcon({
                html: `<div><span>${ feature.properties.point_count_abbreviated }</span></div>`,
                className: `marker-cluster marker-cluster-${ size }`,
                iconSize: L.point(40, 40)
            });

            return L.marker(latlng, {
                icon
            });
        }

    }
});