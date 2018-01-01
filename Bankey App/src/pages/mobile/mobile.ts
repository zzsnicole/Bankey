import { EnterOtpPage } from './../enter-otp/enter-otp';
import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { CountryCode } from "./CountryCode";
import { SelectSearchable } from '../../components/select-searchable/select-searchable';

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
  countryList:any;
  selectedCountry: any = '';
  constructor(public navCtrl: NavController, public navParams: NavParams) {
    this.countryList = new CountryCode().allCountries;
    console.log(this.countryList);
  }

  countryChange(event: { component: SelectSearchable, value: any }) {
      console.log('value:', event.value);
      this.selectedCountry = event.value;
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad MobilePage');
  }

  goToNextPage() {
    this.navCtrl.push(EnterOtpPage);
  }

  typeaheadOnSelect($event) {
    this.selectedCountry = $event.item;
  }
}
