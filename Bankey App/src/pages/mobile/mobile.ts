import { CreatePasswordPage } from './../create-password/create-password';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { CountryCode } from "./CountryCode";

// import { CountryCode } from "./CountryCode";

/**
 * Generated class for the MobilePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-mobile',
  templateUrl: 'mobile.html',
})
export class MobilePage {

  constructor(public navCtrl: NavController, public navParams: NavParams) {

  }
  public countryList = new CountryCode().allCountries;

  selected: string;
  selectedCountry;
  country: any[] = [];

  public get Country(): any {
    return this.country;
  }


  public set Country(v: any) {
    this.country = v;
  }


  ionViewDidLoad() {
    console.log('ionViewDidLoad MobilePage');
    this.formatCountryList();
  }

  public formatCountryList() {
    let formattedListArr = [];
    // _.forEach(this.countryList, element => {
    //   let filterListObj = {
    //     "name": parseInt(element[2]),
    //     "country": element[0],
    //     "countryClass": element[1]
    //   }
    //   formattedListArr.push(filterListObj);
    // });
    this.Country = formattedListArr;
  }
  goToNextPage() {
    this.navCtrl.push(CreatePasswordPage);
  }

  typeaheadOnSelect($event) {
    this.selectedCountry = $event.item;
  }
}
