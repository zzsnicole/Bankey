import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Geolocation } from '@ionic-native/geolocation';
import { Platform } from "ionic-angular";
/*
  Generated class for the LocationServiceProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class LocationServiceProvider {
  userLocation:any={
    "latitude":'',
    "longitude":''
  };
  constructor(public http: HttpClient,
              private geolocation: Geolocation,
              platform: Platform) {
    console.log('Hello LocationServiceProvider Provider');
    platform.ready().then(() =>{
      this.getUserLocation();
    })
  }

  getUserLocation(){
      console.log("user Location called!");
      this.geolocation.getCurrentPosition().then((resp) => {
          this.userLocation.latitude = resp.coords.latitude;
          this.userLocation.longitude = resp.coords.longitude;
          console.log(resp);
      }).catch((error) => {
          console.log('Error getting location', error);
      });
  }

  watchUserLocation(){
      let watch = this.geolocation.watchPosition();
      watch.subscribe((data) => {
          // data can be a set of coordinates, or an error (if an error occurred).
          this.userLocation.latitude = data.coords.latitude;
          this.userLocation.longitude = data.coords.longitude;
      });
  }

}
