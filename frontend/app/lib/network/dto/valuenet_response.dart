class ValueNetResponse {
  final String beams;
  final String potential_values_found_in_db;
  final String question;
  final String question_tokenized;
  final String result;
  final String sem_ql;
  final String sql;

  ValueNetResponse(
      {required this.beams,
      required this.potential_values_found_in_db,
      required this.question,
      required this.question_tokenized,
      required this.result,
      required this.sem_ql,
      required this.sql});

  factory ValueNetResponse.fromJson(Map<String, dynamic> json) {
    return ValueNetResponse(
      beams: json['beams'].toString(),
      potential_values_found_in_db:
          json['potential_values_found_in_db'].toString(),
      question: json['question'].toString(),
      question_tokenized: json['question_tokenized'].toString(),
      result: json['result'].toString(),
      sem_ql: json['sem_ql'].toString(),
      sql: json['sql'].toString(),
    );
  }
}
