package ch.foitt.datahunter

import android.os.Bundle
import android.os.PersistableBundle
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel


class MainActivity : FlutterActivity() {

    private var query: String? = null

    override fun onCreate(savedInstanceState: Bundle?, persistentState: PersistableBundle?) {
        super.onCreate(savedInstanceState, persistentState)
        if (intent.action.equals("actions.intent.GET_THING")) {
            query = intent.getStringExtra("query")
        }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "voiceQuery").setMethodCallHandler {
                call, result ->
            if (call.method == "voiceQueryAssistantCheck") {
              if(query.isNullOrEmpty()){
                  result.error("NONE","No query found",null)
              }else{
                  result.success(query)
              }
            } else {
                result.notImplemented()
            }
        }

        }
    }
