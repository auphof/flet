import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:animated_text_kit/animated_text_kit.dart';

class AnimatedTextKitControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const AnimatedTextKitControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<AnimatedTextKitControl> createState() => _AnimatedTextKitControlState();
}

class _AnimatedTextKitControlState extends State<AnimatedTextKitControl>
    with FletStoreMixin {
  @override
  Widget build(BuildContext context) {
    debugPrint(
        "AnimatedTextKit build: ${widget.control.id} (${widget.control.hashCode})");

    // var src = widget.control.attrString("src", "")!;
    // var srcBase64 = widget.control.attrString("srcBase64", "")!;

    debugPrint("AnimatedTextKit attrString: ${widget.control} ");

    var text = widget.control.attrString("text",
        "text appears to be blank,  so I will just say... Hello world!")!;

    debugPrint("AnimatedTextKit text: ${text} ");

    // if (text == "") {
    //   return const ErrorControl(
    //       "AnimatedTextKit must have \"text\"  specified.");
    // }

    var repeatForever = widget.control.attrBool("repeat_forever", true) ?? true;
    var speed = widget.control.attrInt("speed", 250) ?? 250;
    var pause = widget.control.attrInt("pause", 1000) ?? 1000;

    var displayFullTextOnTap =
        widget.control.attrBool("display_full_text_on_tap", false) ?? false;
    var stopPauseOnTap =
        widget.control.attrBool("stop_pause_on_tap", false) ?? false;
    var isRepeatingAnimation =
        widget.control.attrBool("is_repeating_animation", true) ?? true;
    var totalRepeatCount = widget.control.attrInt("total_repeat_count", 0) ?? 0;
    // var backgroundLoading = widget.control.attrBool("backgroundLoading");
    // var reverse = widget.control.attrBool("reverse");
    // var animate = widget.control.attrBool("animate");
    // var fit = parseBoxFit(widget.control, "fit");
    // FilterQuality filterQuality = FilterQuality.values.firstWhere((e) =>
    //     e.name.toLowerCase() ==
    //     widget.control.attrString("filterQuality", "low")!.toLowerCase());

    void onWarning(String value) {
      if (widget.control.attrBool("onError", false)!) {
        widget.backend.triggerControlEvent(widget.control.id, "error", value);
      }
    }

    return withPageArgs((context, pageArgs) {
      Widget? animatedTextKit;
      animatedTextKit = AnimatedTextKit(
        animatedTexts: [
          TypewriterAnimatedText(
            // 'Hello world!',
            text,
            textStyle: const TextStyle(
              fontSize: 32.0,
              fontWeight: FontWeight.bold,
            ),
            speed: Duration(milliseconds: speed),
          ),
        ],
        isRepeatingAnimation: isRepeatingAnimation,
        repeatForever: repeatForever,
        totalRepeatCount: totalRepeatCount,
        pause: Duration(milliseconds: pause),
        displayFullTextOnTap: displayFullTextOnTap,
        stopPauseOnTap: stopPauseOnTap,
      );
      // TODO: fix this
      // if (text == "") {
      // } else {
      //   var assetSrc = getAssetSrc(src, pageArgs.pageUri!, pageArgs.assetsDir);
      //   if (assetSrc.isFile) {
      //     // Local File
      //     animatedTextKit = AnimatedTextKit.asset(assetSrc.path,
      //         repeat: repeat,
      //         reverse: reverse,
      //         animate: animate,
      //         fit: fit,
      //         filterQuality: filterQuality,
      //         backgroundLoading: backgroundLoading,
      //         onWarning: onWarning);
      //   } else {
      //     // URL
      //     animatedTextKit = AnimatedTextKit.network(assetSrc.path,
      //         repeat: repeat,
      //         reverse: reverse,
      //         animate: animate,
      //         fit: fit,
      //         filterQuality: filterQuality,
      //         backgroundLoading: backgroundLoading,
      //         onWarning: onWarning);
      //   }
      // }

      return constrainedControl(
          context, animatedTextKit, widget.parent, widget.control);
    });
  }
}
