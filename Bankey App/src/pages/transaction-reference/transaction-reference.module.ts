import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { TransactionReferencePage } from './transaction-reference';

@NgModule({
  declarations: [
    TransactionReferencePage,
  ],
  imports: [
    IonicPageModule.forChild(TransactionReferencePage),
  ],
})
export class TransactionReferencePageModule {}
