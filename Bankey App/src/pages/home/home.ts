import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { SignInPage } from "../sign-in/sign-in";
import {SignUpPage} from "../sign-up/sign-up";

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController) {
    
  }
 
  public slides = [
    {
      title: "Create your Bankey Profile",
      description: "Make your own financial profile and check your balance and all your activities on the go",
      image: "assets/img/01_slide.png",
    },
    {
      title: "Get Digital Currency in Exchange for Cash",
      description: "Locate a “key” in your area to withdraw or deposit cash in exchange of digital currency",
      image: "assets/img/02_slide.png",
    },
    {
      title: "Transfer Money Around the Globe Instantly",
      description: "Securely send and receive money anytime and anywhere for FREE",
      image: "assets/img/03_slide.png",
    }
  ];

  public goToNextPage(){
    this.navCtrl.setRoot(SignUpPage);
  }

}
