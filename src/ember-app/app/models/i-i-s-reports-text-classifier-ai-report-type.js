import { buildValidations } from 'ember-cp-validations';
import EmberFlexberryDataModel from 'ember-flexberry-data/models/model';

import {
  defineProjections,
  ValidationRules,
  Model as ReportTypeMixin
} from '../mixins/regenerated/models/i-i-s-reports-text-classifier-ai-report-type';

const Validations = buildValidations(ValidationRules, {
  dependentKeys: ['model.i18n.locale'],
});

let Model = EmberFlexberryDataModel.extend(ReportTypeMixin, Validations, {
});

defineProjections(Model);

export default Model;
