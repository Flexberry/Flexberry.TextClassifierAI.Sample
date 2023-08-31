import { Serializer as ReportTypeSerializer } from
  '../mixins/regenerated/serializers/i-i-s-reports-text-classifier-ai-report-type';
import __ApplicationSerializer from './application';

export default __ApplicationSerializer.extend(ReportTypeSerializer, {
  /**
  * Field name where object identifier is kept.
  */
  primaryKey: '__PrimaryKey'
});
