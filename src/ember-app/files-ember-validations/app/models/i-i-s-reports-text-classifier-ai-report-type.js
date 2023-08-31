import {
  defineNamespace,
  defineProjections,
  Model as ReportTypeMixin
} from '../mixins/regenerated/models/i-i-s-reports-text-classifier-ai-report-type';

import EmberFlexberryDataModel from 'ember-flexberry-data/models/model';

let Model = EmberFlexberryDataModel.extend(ReportTypeMixin, {
});

defineNamespace(Model);
defineProjections(Model);

export default Model;
