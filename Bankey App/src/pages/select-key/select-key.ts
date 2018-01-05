import {Component, ElementRef, ViewChild, NgZone} from '@angular/core';
import { IonicPage, NavController, NavParams, LoadingController } from 'ionic-angular';
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
import {KeyProfilePage} from "../key-profile/key-profile";

declare var google;
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
    @ViewChild('placeSearch')
    public searchElementRef: ElementRef;
    autoComplete:any;
    constructor(public navCtrl: NavController,
                public navParams: NavParams,
                private googleMaps: GoogleMaps,
                private ngZone: NgZone,
                public loadingCtrl: LoadingController) {
    }

    ionViewDidLoad() {
         this.presentLoadingCustom();
         this.getLocation();
         this.loadMap();
         this.autoComplete = new google.maps.places.Autocomplete(this.searchElementRef.nativeElement);

         this.autoComplete.addListener("place_changed", () => {
             this.ngZone.run(() => {
                 //get the place result
                 let place = this.autoComplete.getPlace();

                 //verify result
                 if (place.geometry === undefined || place.geometry === null) {
                     return;
                 }

                 this.map.animateCamera({
                     target: {lat:place.geometry.location.lat(), lng: place.geometry.location.lng()},
                     zoom: 16,
                     tilt: 60,
                     bearing: 140,
                     duration: 5000
                 });
             });
         });
    }

    presentLoadingCustom() {
        let loading = this.loadingCtrl.create({
            spinner: 'hide',
            content: `
        <img style="margin:auto;" class="img-logo" width="30" src="assets/img/logo.png"/>
      <div class="loading-text">
       Looking for Keys..
      </div>
      `,
            duration: 2000
        });

        loading.onDidDismiss(() => {
            console.log('Dismissed loading');
        });

        loading.present();
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
    this.navCtrl.push(KeyProfilePage);
  }
}
