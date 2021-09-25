import 'package:http/http.dart' as http;
import 'dto/valuenet_response.dart';
import 'dart:async';
import 'dart:convert';

class NetworkManager {
  Future<ValueNetResponse> fetchValueNetResponse() async {
    final response = await http.get(
      Uri.parse('https://jsonplaceholder.typicode.com/ValueNetResponses/1'),
    );

    return ValueNetResponse(
        beams: "",
        potential_values_found_in_db: "",
        question: "",
        question_tokenized: "",
        result: "",
        sem_ql: "",
        sql: "");
  }

  Future<ValueNetResponse> updateValueNetResponse(String query) async {
    var url = Uri.parse(
        'https://inference.hackzurich2021.hack-with-admin.ch/api/question/hack_zurich');

    var headers = {
      'Content-Type': 'application/json',
      "X-API-KEY": "sjNmaCtviYzXWlS"
    };
    if (query == "") {
      query = "What is the share of electric cars in 2016 for Wetzikon?";
    }
    // String query_hardcoded = "What is the share of electric cars in 2016 for Wetzikon?";

    final body = {"question": query};

    final response = await http.put(
      url,
      headers: headers,
      body: jsonEncode(body), // use jsonEncode()
    );

    if (response.statusCode == 200) {
      // If the server did return a 200 OK response,
      // then parse the JSON.
      return ValueNetResponse.fromJson(jsonDecode(response.body));
    } else {
      // If the server did not return a 200 OK response,
      // then throw an exception.
      throw Exception('Failed to update ValueNetResponse.');
    }
  }
}
