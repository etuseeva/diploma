import {Injectable} from '@angular/core';
import {ApiService} from '../../services/api.service';

@Injectable()
export class PredictService {
  constructor(private apiService: ApiService) {
  }

}
