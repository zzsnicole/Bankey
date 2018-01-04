import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
/*
  Generated class for the HttpClientProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class HttpClientProvider {
  apiUrl = "http://54.91.82.248/api/";
  constructor(public http: HttpClient) {
    console.log('Hello HttpClientProvider Provider');
  }


  private headers = new HttpHeaders().set('Content-Type','application/json');



  postService(endpoint, data) {
      return new Promise((resolve,reject) => {
          this.http.post(this.apiUrl + endpoint, data,{headers:this.headers}).subscribe(data => {
              resolve(data);
          }, err => {
              reject(err);
              console.log(err);
          });
      });
  }

  getService(endpoint){
      return new Promise(resolve => {
          this.http.get(this.apiUrl + endpoint).subscribe(data => {
              resolve(data);
          }, err => {
              console.log(err);
          });
      });
  }

}