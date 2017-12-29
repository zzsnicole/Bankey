import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import {KeyRequestConfirmPage} from "../key-request-confirm/key-request-confirm";
import {
    GoogleMaps,
    GoogleMap,
    GoogleMapsEvent,
    GoogleMapOptions,
    CameraPosition,
    MarkerOptions,
    Marker
} from '@ionic-native/google-maps';
/**
 * Generated class for the SelectKeyPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-select-key',
  templateUrl: 'select-key.html',
})
export class SelectKeyPage {
    keyLocationsList:any = [];
    map: GoogleMap;
    constructor(public navCtrl: NavController, public navParams: NavParams, private googleMaps: GoogleMaps) {
    }

    ionViewDidLoad() {
        this.getLocation();
        this.loadMap();
    }
    getLocation(){
        this.keyLocationsList = [
            ['Bondi Beach', -33.890542, 151.274856, 4],
            ['Coogee Beach', -33.923036, 151.259052, 5],
            ['Cronulla Beach', -34.028249, 151.157507, 3],
            ['Manly Beach', -33.80010128657071, 151.28747820854187, 2],
            ['Maroubra Beach', -33.950198, 151.259302, 1]
        ];
    }


    loadKeyMarkerOnMap = function(){
        for (let keyLocation of this.keyLocationsList) {
            // Wait the MAP_READY before using any methods.
            console.log(keyLocation);
            console.log(keyLocation);
            this.map.one(GoogleMapsEvent.MAP_READY)
                .then(() => {
                    console.log('Map is ready!');

                    // Now you can use all methods safely.
                    this.map.addMarker({
                        title: keyLocation[0],
                        icon: 'assets/img/custom-marker.png',
                        animation: 'DROP',
                        position: {
                            lat: keyLocation[1],
                            lng: keyLocation[2]
                        }
                    })
                        .then(marker => {
                            marker.on(GoogleMapsEvent.MARKER_CLICK)
                                .subscribe(() => {
                                    // Show the info window
                                    marker.showInfoWindow();
                                    marker.setIcon('assets/img/custom-marker-selected.png');
                                });



                            // Catch the click event
                            marker.on(GoogleMapsEvent.INFO_CLICK, function() {

                                // To do something...
                                alert("Info Clicked!");

                            });
                        });


                });
        }
    }

    loadMap() {

        let mapOptions: GoogleMapOptions = {
            camera: {
                target: {
                    lat: -33.890542,
                    lng: 151.274856
                },
                zoom: 14,
                tilt: 30
            },
            controls: {
                'compass': true,
                'myLocationButton': true,
                'indoorPicker': true,
                'zoom': true // Only for Android
            },
            gestures: {
                'scroll': true,
                'tilt': true,
                'rotate': true,
                'zoom': true
            }
        };

        this.map = this.googleMaps.create('map_canvas', mapOptions);
        this.loadKeyMarkerOnMap();
    }

  GoConfirmKey() {
    this.navCtrl.push(KeyRequestConfirmPage);
  }
}
