package {{JAVA_PACKAGE}};

import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("{{ROUTE_PREFIX}}")
public class RiskController {

    @PostMapping("/evaluate")
    public ResponseEntity<?> evaluate(@RequestBody Map<String, Object> body) {
        // TODO: Parse model + input and call evaluator service.
        return ResponseEntity.badRequest().body(Map.of("status", 1, "error", "connect evaluator", "version", 0));
    }

    @PostMapping("/evaluate-all")
    public ResponseEntity<?> evaluateAll(@RequestBody Map<String, Object> body) {
        // TODO: Parse input and call evaluator-all service.
        return ResponseEntity.ok(Map.of("error", "connect evaluator"));
    }
}
