import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:animated_text_kit/animated_text_kit.dart';

import 'package:flet/src/utils/text.dart';
// import 'package:flet/src/utils/theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class AnimatedTextKitControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final Widget? nextChild;
  final FletControlBackend backend;

  // final List<dynamic> animatedTextsConfig;

  const AnimatedTextKitControl({
    super.key,
    required this.parent,
    required this.control,
    required this.children,
    required this.nextChild,
    required this.parentDisabled,
    required this.parentAdaptive,
    required this.backend,
    // required this.animatedTextsConfig
  });

  @override
  State<AnimatedTextKitControl> createState() => _AnimatedTextKitControlState();
}

class _AnimatedTextKitControlState extends State<AnimatedTextKitControl>
    with FletStoreMixin {
  String _text = "";
  // bool _revealPassword = false;
  bool _focused = false;
  // late TextEditingController _controller;
  late final FocusNode _focusNode;
  late final FocusNode _shiftEnterfocusNode;
  String? _lastFocusValue;
  @override
  void initState() {
    super.initState();
    // _controller = TextEditingController();
    _shiftEnterfocusNode = FocusNode(
      onKeyEvent: (FocusNode node, KeyEvent evt) {
        if (!HardwareKeyboard.instance.isShiftPressed &&
            evt.logicalKey.keyLabel == 'Enter') {
          if (evt is KeyDownEvent) {
            widget.backend.triggerControlEvent(widget.control.id, "submit");
          }
          return KeyEventResult.handled;
        } else {
          return KeyEventResult.ignored;
        }
      },
    );
    _shiftEnterfocusNode.addListener(_onShiftEnterFocusChange);
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    // _controller.dispose();
    _shiftEnterfocusNode.removeListener(_onShiftEnterFocusChange);
    _shiftEnterfocusNode.dispose();
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onShiftEnterFocusChange() {
    setState(() {
      _focused = _shiftEnterfocusNode.hasFocus;
    });
    widget.backend.triggerControlEvent(widget.control.id,
        _shiftEnterfocusNode.hasFocus ? "focus" : "blur", "");
  }

  void _onFocusChange() {
    setState(() {
      _focused = _focusNode.hasFocus;
    });
    widget.backend.triggerControlEvent(
        widget.control.id, _focusNode.hasFocus ? "focus" : "blur", "");
  }

  List<AnimatedText> _createAnimatedTexts(
      String animatedTextsConfig, TextStyle? defaultTextStyle) {
    // Decode the JSON and ensure it's properly cast.
    List<dynamic> configs;

    try {
      configs = json.decode(animatedTextsConfig) as List<dynamic>;
    } catch (e) {
      throw Exception('Error decoding JSON: $e');
    }

    return configs.map<AnimatedText>((dynamic config) {
      // Ensure each config is a proper Map.
      if (config is! Map) {
        throw Exception(
            'Each config must be a map. Found: ${config.runtimeType}');
      }
      Map<String, dynamic> mapConfig = config.cast<String, dynamic>();

      // Extract and validate required fields.
      String type = mapConfig['type'];
      String text = mapConfig['text'];
      int? durationMs = mapConfig['duration_ms'];

      if (type == null || text == null || durationMs == null) {
        throw Exception(
            'Missing required config keys or invalid types: type, text, or duration_ms.');
      }

      switch (config['type']) {
        case 'Typewriter':
          return TypewriterAnimatedText(
            config['text'],
            // TODO TD: the following test for Null should not be required , it should inherit if not set
            // see child: DefaultTextStyle( in https://github.com/aagarwal1012/Animated-Text-Kit/tree/master?tab=readme-ov-file#typewriter
            textStyle: config['textStyle'] ?? defaultTextStyle,
            speed: Duration(milliseconds: config['duration_ms']),
          );
        case 'Rotate':
          return RotateAnimatedText(
            config['text'],
            // TODO TD: the following test for Null should not be required , it should inherit if not set
            // see child: DefaultTextStyle( in https://github.com/aagarwal1012/Animated-Text-Kit/tree/master?tab=readme-ov-file#typewriter
            textStyle: config['textStyle'] ?? defaultTextStyle,
            duration: Duration(milliseconds: config['duration_ms']),
            rotateOut: config['rotate_out'] ?? false,
          );
        case 'Fade':
          return FadeAnimatedText(
            config['text'],
            // TODO TD: the following test for Null should not be required , it should inherit if not set
            // see child: DefaultTextStyle( in https://github.com/aagarwal1012/Animated-Text-Kit/tree/master?tab=readme-ov-file#typewriter
            textStyle: config['textStyle'] ?? defaultTextStyle,
            duration: Duration(milliseconds: config['duration_ms']),
            fadeInEnd: config['fade_in_end'] ?? 0.5,
            fadeOutBegin: config['fade_out_begin'] ?? 0.8,
          );
        case 'Scale':
          return ScaleAnimatedText(config['text'],
              // TODO TD: the following test for Null should not be required , it should inherit if not set
              // see child: DefaultTextStyle( in https://github.com/aagarwal1012/Animated-Text-Kit/tree/master?tab=readme-ov-file#typewriter
              textStyle: config['textStyle'] ?? defaultTextStyle,
              duration: Duration(milliseconds: config['duration_ms']),
              scalingFactor: config['scalingFactor'] ?? 0.5
              // fadeIn: config['fade_in'] ?? true,
              );
        // Add more cases as needed
        default:
          throw Exception('Unsupported animation type: ${config['type']}');
      }
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "AnimatedTextKit build: ${widget.control.id} (${widget.control.hashCode})");
    return withPagePlatform((context, platform) {
      bool autofocus = widget.control.attrBool("autofocus", false)!;
      bool disabled = widget.control.isDisabled || widget.parentDisabled;

      bool? adaptive =
          widget.control.attrBool("adaptive") ?? widget.parentAdaptive;
      // if (adaptive == true &&
      //     (platform == TargetPlatform.iOS ||
      //         platform == TargetPlatform.macOS)) {
      //   return CupertinoTextFieldControl(
      //       control: widget.control,
      //       children: widget.children,
      //       parent: widget.parent,
      //       parentDisabled: widget.parentDisabled,
      //       parentAdaptive: adaptive,
      //       backend: widget.backend);
      // }

      // bool disabled = control.isDisabled || parentDisabled;
      // var src = widget.control.attrString("src", "")!;
      // var srcBase64 = widget.control.attrString("srcBase64", "")!;

      debugPrint("AnimatedTextKit attrString: ${widget.control} ");

      // var prefixControls =
      //     widget.children.where((c) => c.name == "prefix" && c.isVisible);
      // var suffixControls =
      //     widget.children.where((c) => c.name == "suffix" && c.isVisible);

      var cursorColor = widget.control.attrColor("cursorColor", context);
      var selectionColor = widget.control.attrColor("selectionColor", context);

      var textSize = widget.control.attrDouble("textSize");

      var color = widget.control.attrColor("color", context);
      var focusedColor = widget.control.attrColor("focusedColor", context);

      var theme = Theme.of(context);

      var textStyleTest = widget.control.attrString("textStyle");
      debugPrint("AnimatedTextKit textStyleTest: ${textStyleTest} ");
      TextStyle? textStyle = parseTextStyle(theme, widget.control, "textStyle");
      // TextStyle? textStyle = TextStyle(
      //   fontSize: 32.0,
      //   fontWeight: FontWeight.bold,
      // );
      debugPrint("AnimatedTextKit textStyle: ${textStyle} ");

      if (textSize != null || color != null || focusedColor != null) {
        textStyle = (textStyle ?? const TextStyle()).copyWith(
            fontSize: textSize,
            color: _focused ? focusedColor ?? color : color);
      }
      debugPrint("AnimatedTextKit style: ${textStyle} ");
      // debugPrint("AnimatedTextKit text: ${text} ");

      // if (text == "") {
      //   return const ErrorControl(
      //       "AnimatedTextKit must have \"text\"  specified.");
      // }

      var repeatForever =
          widget.control.attrBool("repeat_forever", true) ?? true;
      var speed = widget.control.attrInt("speed", 250) ?? 250;
      var pause = widget.control.attrInt("pause", 1000) ?? 1000;

      var displayFullTextOnTap =
          widget.control.attrBool("display_full_text_on_tap", false) ?? false;
      var stopPauseOnTap =
          widget.control.attrBool("stop_pause_on_tap", false) ?? false;
      var isRepeatingAnimation =
          widget.control.attrBool("is_repeating_animation", true) ?? true;
      var totalRepeatCount =
          widget.control.attrInt("total_repeat_count", 0) ?? 0;
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

      bool shiftEnter = widget.control.attrBool("shiftEnter", false)!;
      FocusNode focusNode = shiftEnter ? _shiftEnterfocusNode : _focusNode;
      var focusValue = widget.control.attrString("focus");
      if (focusValue != null && focusValue != _lastFocusValue) {
        _lastFocusValue = focusValue;
        focusNode.requestFocus();
      }
      String animatedTextsConfig = widget.control.attrString("animatedTexts")!;
      debugPrint(
          "AnimatedTextKit animatedTextsConfig: ${animatedTextsConfig} ");
      var animatedTexts = _createAnimatedTexts(animatedTextsConfig, textStyle);
      debugPrint("AnimatedTextKit animatedTexts: ${animatedTexts} ");
      bool onFinishedCallback = widget.control.attrBool("onFinished", false)!;
      debugPrint(
          "AnimatedTextKit ASSERT 3 ------------ assert(null == onFinished || !repeatForever), : onFinished: ${onFinishedCallback}, repeatForever: ${repeatForever}");
      Widget animatedTextKit = AnimatedTextKit(
        // autofocus: autofocus,
        // enabled: !disabled,
        animatedTexts: animatedTexts,

        isRepeatingAnimation: isRepeatingAnimation,
        repeatForever: repeatForever,
        totalRepeatCount: totalRepeatCount,
        pause: Duration(milliseconds: pause),
        displayFullTextOnTap: displayFullTextOnTap,
        stopPauseOnTap: stopPauseOnTap,
        onTap: () {
          debugPrint("AnimatedTextKit ${widget.control.id} onTap!");
          widget.backend.triggerControlEvent(widget.control.id, "on_tap");
        },
        onFinished: onFinishedCallback
            ? () {
                debugPrint("AnimatedTextKit ${widget.control.id} onFinished!");
                widget.backend
                    .triggerControlEvent(widget.control.id, "on_finished");
              }
            : null,

        onNext: (int, bool) {
          debugPrint("AnimatedTextKit ${widget.control.id} onNext!");
          widget.backend.triggerControlEvent(widget.control.id, "on_next");
        },
        onNextBeforePause: (int, bool) {
          debugPrint("AnimatedTextKit ${widget.control.id} onNextBeforePause!");
          widget.backend
              .triggerControlEvent(widget.control.id, "on_next_before_pause");
        },
      );

      if (cursorColor != null || selectionColor != null) {
        animatedTextKit = TextSelectionTheme(
            data: TextSelectionTheme.of(context).copyWith(
                cursorColor: cursorColor, selectionColor: selectionColor),
            child: animatedTextKit);
      }

      if (widget.control.attrInt("expand", 0)! > 0) {
        return constrainedControl(
            context, animatedTextKit, widget.parent, widget.control);
      } else {
        return LayoutBuilder(
          builder: (BuildContext context, BoxConstraints constraints) {
            if (constraints.maxWidth == double.infinity &&
                widget.control.attrDouble("width") == null) {
              animatedTextKit = ConstrainedBox(
                constraints: const BoxConstraints.tightFor(width: 300),
                child: animatedTextKit,
              );
            }

            return constrainedControl(
                context, animatedTextKit, widget.parent, widget.control);
          },
        );
      }
    });
  }
}
