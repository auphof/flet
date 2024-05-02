import 'package:flet/flet.dart';

import 'animated_text_kit.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "animated_text_kit":
      return AnimatedTextKitControl(
          parent: args.parent,
          control: args.control,
          children: args.children,
          parentDisabled: args.parentDisabled,
          parentAdaptive: args.parentAdaptive,
          nextChild: args.nextChild,
          backend: args.backend);
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
