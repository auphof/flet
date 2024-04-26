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
    var text = widget.control.attrString("text",
        "text appears to be blank,  so I will just say... Hello world!")!;

    // if (text == "") {
    //   return const ErrorControl(
    //       "AnimatedTextKit must have \"text\"  specified.");
    // }

    var repeat = widget.control.attrBool("repeat", true);
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
            speed: const Duration(milliseconds: 500),
          ),
        ],
        totalRepeatCount: 4,
        pause: const Duration(milliseconds: 1000),
        displayFullTextOnTap: true,
        stopPauseOnTap: true,
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
