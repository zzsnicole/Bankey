import { PersonalDetailsPage } from './../personal-details/personal-details';
import {
  Component, ViewChild
  , ElementRef
} from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

/**
 * Generated class for the EnterOtpPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@Component({
  selector: 'page-enter-otp',
  templateUrl: 'enter-otp.html',
})
export class EnterOtpPage {

  headerLabel = 'Enter the 6-digit code';
  enteredOTP = '';
  otp = "";


  @ViewChild('input') input: ElementRef;
  @ViewChild('inputHidden') inputHidden: ElementRef;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  onKeyup(event) {
    console.log(this.otp.length)
    if (this.otp.length == 6) {
      // console.log('666')
      // debugger
      // if(this.inputHidden){
      //   this.inputHidden.nativeElement.focus();
      // }
      
      // var e = new Event('blur')
      // this.input.nativeElement.dispatchEvent(e);
    }

  }

  goToNextPage() {
    console.log('next page');
    this.navCtrl.push(PersonalDetailsPage);
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EnterOtpPage');
  }


}
