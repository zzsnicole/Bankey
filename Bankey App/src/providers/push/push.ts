import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FCM } from '@ionic-native/fcm';
import { Platform } from "ionic-angular";

/*
  Generated class for the PushProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class PushProvider {

  constructor(public http: HttpClient,
              private fcm: FCM,
              platform: Platform) {
    console.log('Hello PushProvider Provider');
    platform.ready().then(() => {
        this.init();
    });
  }

  init(){
      this.fcm.getToken().then(token=>{
          console.log("getToken");
          console.log(token);
      });
      this.fcm.onTokenRefresh().subscribe(token=>{
          console.log("onTokenRefresh");
          console.log(token);
      })
      this.fcm.onNotification().subscribe(data=>{
          console.log(data);
          if(data.wasTapped){
              console.log("Received in background");
          } else {
              console.log("Received in foreground");
          };
      })
  }

}
